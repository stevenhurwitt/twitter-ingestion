terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  region  = "us-east-2"
}

resource "aws_instance" "twitter" {
  ami           = "ami-0ff596d41505819fd"
  instance_type = "t4g.xlarge"

  tags = {
    Name = "twitter"
  }
}
