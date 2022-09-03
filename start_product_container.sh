docker stop prod_container
docker rm prod_container
docker rmi prod_container
docker build -t productproject productproject
sudo docker run -d --name prod_container -p 8000:8000 productproject
