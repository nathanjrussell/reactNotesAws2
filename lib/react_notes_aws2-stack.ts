import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as iam from 'aws-cdk-lib/aws-iam'; // Import IAM

export class ReactNotesAws2Stack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, { 
      ...props, env: {account: '360228089988'}
    });

    const lambdaRole = new iam.Role(this, 'LambdaRole', {
      assumedBy: new iam.ServicePrincipal('lambda.amazonaws.com'),
    });
    const policyName = 'arn:aws:iam::360228089988:policy/service-role/AWSLambdaMicroserviceExecutionRole-254f80b2-c0c1-402a-9974-6b1d31eab1e6';
    lambdaRole.addManagedPolicy(iam.ManagedPolicy.fromManagedPolicyArn(this, 'CustomPolicy', policyName));

    const lambdaFunction = new lambda.Function(this, 'LambdaFunction', {
      runtime: lambda.Runtime.PYTHON_3_12,
      code: lambda.Code.fromAsset('lambda'),
      handler: "getMenu.lambda_handler",
      role: lambdaRole, // Assign the role here
    });

  }

}