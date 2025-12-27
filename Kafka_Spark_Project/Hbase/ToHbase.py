import happybase

def write_to_hbase(batch_df, batch_id):
    connection = happybase.Connection('localhost')  
    table = connection.table('web_logs')
    
    for row in batch_df.collect():
        table.put(
            row['ip'],  # Row key
            {
                b'LOG:timestamp': row['timestamp'].encode('utf-8'),
                b'LOG:method': row['method'].encode('utf-8'),
                b'LOG:url': row['url'].encode('utf-8'),
                b'LOG:status': row['status'].encode('utf-8'),
                b'LOG:size': row['size'].encode('utf-8')
            }
        )
    connection.close()

query_hbase = parsed.writeStream \
    .foreachBatch(write_to_hbase) \
    .outputMode("append") \
    .start()

