for i in * ; do
    if [ -d "$i" ]; then
        pep8 --exclude=const.py "$i"
    fi
done
