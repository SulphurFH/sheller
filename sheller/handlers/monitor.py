from sheller import redis_connection, models, __version__
from sheller.handlers.base import BaseResource


def get_redis_status():
    info = redis_connection.info()
    return {'redis_used_memory': info['used_memory'], 'redis_used_memory_human': info['used_memory_human']}


def get_db_sizes():
    database_metrics = []
    metrics_sql = "SELECT CONCAT(table_schema,'.',table_name) AS 'Table Name', \
                   CONCAT(ROUND(table_rows/1000000,4),'M') AS 'Number of Rows', \
                   CONCAT(ROUND(data_length/(1024*1024*1024),4),'G') AS 'Data Size', \
                   CONCAT(ROUND(index_length/(1024*1024*1024),4),'G') AS 'Index Size', \
                   CONCAT(ROUND((data_length+index_length)/(1024*1024*1024),4),'G') AS'Total' \
                   FROM information_schema.TABLES WHERE table_schema LIKE 'sheller'"
    queries = [
        ['Sheller DB Size', metrics_sql]
    ]
    for query_name, query in queries:
        titles = models.db.session.execute(query).keys()
        results = models.db.session.execute(query).fetchall()
        info = []
        for item in results:
            info.append(dict(zip(titles, item)))
        database_metrics.append([query_name, info])

    return database_metrics


class MonitorResource(BaseResource):
    def get(self):
        status = {
            'version': __version__,
        }
        status.update(get_redis_status())
        status['database_metrics'] = {}
        status['database_metrics']['metrics'] = get_db_sizes()

        return status
