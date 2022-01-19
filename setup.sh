

START_CRAWLER='n'
END_CRAWLER='n'
START_VUE_APP='n'

if [ $# -eq 0 ]
then
    echo "Please add command"
else    
    for arg in "$@"
    do        
        if [ "$arg" == '-up' ] || [ "$arg" == '-r' ]
        then
            START_CRAWLER='y'
            echo "Start Web Crawler"        
        elif [ "$arg" == '-down' ] || [ "$arg" == '-d' ]
        then
            END_CRAWLER='y'
            echo "End Web Crawler"
        elif [ "$arg" == '-vue' ] || [ "$arg" == '-rf' ]
        then
            START_VUE_APP='y'
        fi
    done
fi

if [ $START_CRAWLER == 'y' ]
then
    docker-compose build --no-cache
    docker-compose up -d
fi

if [ $END_CRAWLER == 'y' ]
then
    docker-compose down --rmi all -v
fi

if [ $START_VUE_APP == 'y' ]
then
    cd crawler-app 
    npm install
    npm run dev
fi