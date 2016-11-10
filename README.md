# resource_monitoring
do resource monitoring

Agent-oriented system
- CPU
- memory
- disk
- network

Web resource monitoring:
- github
- redmain
- wiki

Finally we would like to see resources under differnt PC (controlled by agent) and web resources

#run web
python app.py

#run celery
#celery -A tasks worker --loglevel=debug
celery worker -l debug -A tasks --beat
