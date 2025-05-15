#!/bin/bash
#
# Script to fix Django migration issues related to the "user" column in the
# image_upload_image table.  This script assumes a PostgreSQL database
# with the following settings:
#
# Database Settings:
#
# ENGINE:   django.db.backends.postgresql
# NAME:     realreview_db
# USER:     dev
# PASSWORD: ''  (Empty password)
# HOST:     localhost
# PORT:     5432
#
# Prerequisites:
#
# * PostgreSQL is installed and running.
# * You have the 'psql' command-line tool available.
# * You are running this script in the same environment as your
#     Django project (i.e., where 'manage.py' is located).
# * You have activated your virtual environment (if you are using one).
#
# WARNING: This script may modify your database.  It is HIGHLY
#          RECOMMENDED to have a recent backup of your database
#          before running this script.
#
# Variables: (Customize these if necessary)
PG_USER="dev"
PG_DATABASE="realreview_db"
BACKUP_FILE="migration_fix_backup.sql"
DJANGO_MANAGE_PY="../manage.py"  #  Path to your manage.py (relative to scripts/)
MIGRATION_BEFORE="0004"       #  The migration *before* the problematic one
MIGRATION_PROBLEM="0005"      #  The problematic migration
# Function to display messages
log_info() {
    echo -e "\e[34mINFO: $1\e[0m" # Blue
}

log_warning() {
    echo -e "\e[33mWARNING: $1\e[0m" # Yellow
}

log_error() {
    echo -e "\e[31mERROR: $1\e[0m" # Red
}

log_success() {
    echo -e "\e[32mSUCCESS: $1\e[0m" # Green
}
# 1. Backup Your Database
#
log_info "1. Backing up the database..."
log_info "   Creating backup: $BACKUP_FILE"
pg_dump -U "$PG_USER" -d "$PG_DATABASE" -f "$BACKUP_FILE"
if [ $? -eq 0 ]; then
    log_success "   Database backup created successfully: $BACKUP_FILE"
else
    log_error "   Failed to create database backup.  Exiting."
    exit 1
fi

# 2. Drop the image_upload_image table
#
log_info "2. Dropping the image_upload_image table..."
PGPASSWORD='' psql -U "$PG_USER" -d "$PG_DATABASE" -c "DROP TABLE IF EXISTS image_upload_image CASCADE;"
if [ $? -eq 0 ]; then
    log_success "   image_upload_image table dropped."
else
    log_error "   Failed to drop image_upload_image table.  Exiting."
    exit 1
fi

# 3.  Clear the django_migrations entry for image_upload
#
log_info "3.  Clearing the django_migrations entry for image_upload..."
PGPASSWORD='' psql -U "$PG_USER" -d "$PG_DATABASE" -c "DELETE FROM django_migrations WHERE app='image_upload';"
if [ $? -eq 0 ]; then
    log_success "   Cleared django_migrations entry for image_upload."
else
    log_warning "   Failed to clear django_migrations entry for image_upload.  Continuing anyway..."
fi



# 4. Apply migrations
#
log_info "4. Applying migrations..."
log_info "   Applying all migrations..."
python "$DJANGO_MANAGE_PY" migrate
if [ $? -eq 0 ]; then
    log_success "   Migrations applied successfully."
else
    log_error "   Failed to apply migrations.  Please check for errors.  Exiting."
    exit 1
fi

# 5. Verify the Database Again
#
log_info "5. Verifying database state after migration..."
log_info "   Connecting to PostgreSQL and describing the image_upload_image table..."
psql -U "$PG_USER" -d "$PG_DATABASE" -c "\d image_upload_image;" > temp_db_description.txt 2>&1

user_column_name=$(grep "user" temp_db_description.txt | awk '{print $1}')
user_column_type=$(grep "user" temp_db_description.txt | awk '{print $2}')
fk_constraint=$(grep "FOREIGN KEY" temp_db_description.txt)

rm temp_db_description.txt
if [[ "$user_column_name" == "user_id" && "$user_column_type" == "integer" ]] && [[ ! -z "$fk_constraint" ]]; then
    log_success "   'user_id' column is an integer and has a foreign key constraint as expected."
else
    log_error "   'user' column is not an integer or does not have a foreign key.  Migration was not successful. Exiting."
    exit 1
fi

# 6. Run the data migration to link images to users
log_info "6. Running data migration to link images to users..."
python "$DJANGO_MANAGE_PY" shell -c "from django.apps import apps; from fix_image_user_field_migration import link_images_to_users; link_images_to_users(apps, None)"

if [ $? -eq 0 ]; then
    log_success "   Data migration ran successfully."
else
    log_error "   Data migration failed.  Please check for errors."
    exit 1
fi

# 7. Check for orphaned records
log_info "7. Checking for orphaned records in image_upload_image table..."
orphaned_records=$(psql -U "$PG_USER" -d "$PG_DATABASE" -c "SELECT count(*) FROM image_upload_image i LEFT JOIN auth_user u ON i.user_id = u.id WHERE u.id IS NULL;" | grep -Po '^\s*\d+\s*$')

if [[ "$orphaned_records" -gt 0 ]]; then
    log_warning "   Found $orphaned_records orphaned records.  You MUST address these manually."
    log_warning "   Orphaned records have image_upload_image.user_id values that do not exist in auth_user.id."
    log_warning "   You can either delete these image_upload_image records, or update them to point to a valid user_id."
    log_warning "   Exiting without further automated changes."
    exit 1
else
    log_success "   No orphaned records found."
fi

log_success "   Database schema is now consistent with Django models."
log_info "   Migration process completed."
exit 0

