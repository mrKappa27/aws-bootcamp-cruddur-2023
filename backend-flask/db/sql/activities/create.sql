INSERT INTO public.activities (
  user_uuid,
  message,
  expires_at
)
VALUES (
  %(handle)s,
  %(message)s,
  %(expires_at)s
) RETURNING uuid;