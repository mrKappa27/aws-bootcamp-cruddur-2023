INSERT INTO public.users (display_name, handle, cognito_user_id)
VALUES
  ('KevvoRT', 'kevvort' ,'78919c1f-d161-46e3-874d-cbe9facfc915'),
  ('Andrew Bayko', 'bayko' ,'MOCK');

INSERT INTO public.activities (user_uuid, message, expires_at)
VALUES
  (
    (SELECT uuid from public.users WHERE users.handle = 'kevvort' LIMIT 1),
    'This was imported as seed data!',
    current_timestamp + interval '10 day'
  )