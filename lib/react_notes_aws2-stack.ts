import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as apigateway from 'aws-cdk-lib/aws-apigateway';
import { env } from 'process';
export class ReactNotesAws2Stack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, { 
      ...props, env: {account: '360228089988'}
    });
    
    const lambdaFunction = new lambda.Function(this, 'LambdaFunction', {
      runtime: lambda.Runtime.PYTHON_3_12,
      code: lambda.Code.fromAsset('lambda'),
      handler: "main.handler"
    });

    /**
     * Represents the API Gateway for the React Notes application.
     */
    const api = new apigateway.RestApi(this, 'ApiGateway', {
      restApiName: 'ReactNotesApiGateway',
      description: 'This is my lambda function',
    });

    const notesResource = api.root.addResource('notes');
    notesResource.addMethod('GET', new apigateway.LambdaIntegration(lambdaFunction));

    // const functionUrl = lambdaFunction.addFunctionUrl( {
    //   authType: lambda.FunctionUrlAuthType.NONE,
    //   cors: {
    //     allowedOrigins: ['*'],
    //     allowedMethods: [lambda.HttpMethod.ALL],
    //     allowedHeaders: ['*'],
    //   }
    // });

    // new cdk.CfnOutput(this, 'Url', { 
    //   value: functionUrl.url,
    // });
  }

}
