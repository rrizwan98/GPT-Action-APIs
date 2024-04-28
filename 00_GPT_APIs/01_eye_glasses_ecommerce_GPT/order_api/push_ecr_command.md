Deploy our API in AWS App Runner:

First, you need to deploy the Docker container to the AWS ECR repository, and then connect this ECR repository to the AWS App Runner.

Steps to push Docker container to AWS ECR:

1. Run: `aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 220544705075.dkr.ecr.us-east-2.amazonaws.com`
2. Build the Docker image: `docker build -t eye-glasses-ecommerce-gpt:1.0.0 .`
3. Tag the Docker image: `docker tag eye-glasses-ecommerce-gpt:1.0.0 220544705075.dkr.ecr.us-east-2.amazonaws.com/eye-glasses-ecommerce-gpt:1.0.0`
4. Push the Docker image to the repository: `docker push 220544705075.dkr.ecr.us-east-2.amazonaws.com/eye-glasses-ecommerce-gpt:1.0.0`

Deploy ECR repository to AWS App Runner:

Watch the tutorial on YouTube: [YouTube Tutorial](https://www.youtube.com/watch?v=TKirecwhJ2c)