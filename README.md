# Sheller

## Development

./bin/run_development

## Production
gunicorn -b 0.0.0.0:5000 --name sheller -w 6 sheller.wsgi:app
