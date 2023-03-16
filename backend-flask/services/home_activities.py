from datetime import datetime, timedelta, timezone
from opentelemetry import trace
import sys, random

#Database
from lib.db import pool, query_wrap_array

# Honeycomb tracer
tracer = trace.get_tracer("home.activities")

results = []

class HomeActivities:
  def run(logger, cognito_user_id=None):  
    #results = {}
    logger.info('home_activities - BEGIN')
    with tracer.start_as_current_span("home.activities.mock-data"):
      span = trace.get_current_span()
      now = datetime.now(timezone.utc).astimezone()
      ## Application timestamp at start span
      #span.set_attribute("app.now", now.isoformat())
      #if cognito_user_id != None:
      #  span.set_attribute("app.user_id", cognito_user_id)
      #else:
      #  span.set_attribute("app.user_id", 0)

      # Database fetch
      sql = query_wrap_array("""
        SELECT
          activities.uuid,
          users.display_name,
          users.handle,
          activities.message,
          activities.replies_count,
          activities.reposts_count,
          activities.likes_count,
          activities.reply_to_activity_uuid,
          activities.expires_at,
          activities.created_at
        FROM public.activities
        LEFT JOIN public.users ON users.uuid = activities.user_uuid
        ORDER BY activities.created_at DESC
      """)
    
      with pool.connection() as conn:
        with conn.cursor() as cur:
          cur.execute(sql)
          # this will return a tuple
          # the first field being the data
          json = cur.fetchone()
          print(json)
      #return json[0]

      span.set_attribute("app.result_lenght_byte", sys.getsizeof(json))
      span.set_attribute("app.result_lenght", len(json))

      return json[0]