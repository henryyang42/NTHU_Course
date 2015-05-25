for i in * ; do
    if [ -d "$i" ]; then
        pep8 "$i"
    fi
done
