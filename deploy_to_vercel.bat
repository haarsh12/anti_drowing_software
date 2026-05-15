@echo off
echo Deploying Anti-Drowning Dashboard to Vercel...

cd frontend_anti

echo Installing dependencies...
npm install

echo Building project...
npm run build

echo Deploying to Vercel...
npx vercel --prod

echo Deployment complete!
echo Check your Vercel dashboard for the live URL.

pause