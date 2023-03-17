from datetime import datetime, timedelta, timezone
from opentelemetry import trace
import sys

#Database
from lib.db import db

# Honeycomb tracer
tracer = trace.get_tracer("home.activities")

results = []

class HomeActivities:
  def run(logger, cognito_user_id=None):  
    logger.info('home_activities - BEGIN')
    with tracer.start_as_current_span("home.activities.mock-data"):
      span = trace.get_current_span()
      now = datetime.now(timezone.utc).astimezone()

      # Application timestamp at start span
      span.set_attribute("app.now", now.isoformat())
      
      ##TODO: Add this if you want to check that the user is logged in or not
      ##if cognito_user_id != None:
      ##  span.set_attribute("app.user_id", cognito_user_id)
      ##else:
      ##  span.set_attribute("app.user_id", 0)

      # Database fetch
      sql = db.template('activities','home')
      results = db.query_array_json(sql)
      
      span.set_attribute("app.result_lenght_byte", sys.getsizeof(results))
      span.set_attribute("app.result_lenght", len(results))

      return results