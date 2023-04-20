INSERT INTO public.users (display_name, email, handle, cognito_user_id)
VALUES
  ('KevvoRT', 'kevvort@hotmail.it', 'kevvort', 'MOCK'),
  ('Andrew Bayko', 'bayko@exampro.co', 'bayko', 'MOCK'),
  ('Mondo Lollari', 'mlollari@acme.co', 'lollari', 'MOCK');

INSERT INTO public.activities (user_uuid, message, expires_at)
VALUES
  (
    (SELECT uuid from public.users WHERE users.handle = 'kevvort' LIMIT 1),
    'This was imported as seed data!',
    current_timestamp + interval '10 day'
  )