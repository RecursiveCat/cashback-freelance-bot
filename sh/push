echo "BACKUP..."
cd .. && mkdir backup && cp -r pwd backup
echo "UPDATES DOWNLOADING FROM GITHUB..."
cd - && git pull
echo "ADDING NEW UPDATES..."
git add -A
echo "COMMITING UPDATES..."
git commit -m "push from script"
echo "PUSH UPDATES..."
git push
