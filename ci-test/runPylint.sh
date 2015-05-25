for i in * ; do
    if [ -d "$i" ]; then
        pylint --load-plugins pylint_django "$i"
    fi
done
