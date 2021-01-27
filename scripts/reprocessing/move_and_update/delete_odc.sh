# This doesn't work in vdi
#module load agdc-py3/1.1.8

psql -h dea-db.nci.org.au dsg547 -d dsg547_dev -a -f db_delete_odc.sql
