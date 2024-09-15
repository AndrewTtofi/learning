# CrossFit Workout Fetcher

This project fetches the latest CrossFit workout from the CrossFit website, parses the workout content, and serves it as a JSON response via an AWS Lambda function. The AWS Lambda function uses a layer to manage dependencies (`requests` and `beautifulsoup4`).

## Features

- Fetches and parses the latest CrossFit workout from the CrossFit website.
- Returns the workout in a structured JSON format.
- Uses AWS Lambda to serve the workout data.
- Dependencies are managed via AWS Lambda layers for efficiency.

## Prerequisites

- Python 3.x installed on your local machine.
- AWS CLI configured with access to your AWS account.
- Basic knowledge of AWS Lambda and AWS API Gateway.

## Project Structure

```bash
├── lambda_function.py       # Main Python script for AWS Lambda
├── requirements.txt         # List of dependencies
├── README.md                # Project documentation
├── lambda_layer/            # Directory for AWS Lambda Layer
│   └── python/              # Directory structure for dependencies
│       ├── requests/        # Installed requests library
│       ├── bs4/             # Installed beautifulsoup4 library
└── layer.zip                # Zipped layer for AWS Lambda
```

## How to Run Locally

1. **Clone the Repository**:

```bash
 git clone https://github.com/AndrewTtofi/learning.git
 cd learning/python-crossfit/crossfit-workout-fetcher
```

2. **Set Up a Virtual Environment**:

   Create and activate a virtual environment to manage dependencies locally:

   ```bash
   python -m venv env
   source env/bin/activate   # On Windows, use `.\env\Scripts\activate`
   ```

3. **Install Dependencies**:

   Install the required Python libraries:

   ```bash
   pip install requests beautifulsoup4
   ```

4. **Run the Python Script**:

   Run the Python script to fetch and parse the workout data locally:

   ```bash
   python lambda_function.py
   ```

## How to Deploy to AWS Lambda

### Step 1: Create a Lambda Layer for Dependencies

1. **Create a Directory Structure for the Layer**:

   ```bash
   mkdir lambda_layer
   cd lambda_layer
   mkdir python
   ```

2. **Install Dependencies into the `python` Directory**:

   ```bash
   pip install requests beautifulsoup4 -t python/
   ```

3. **Zip the Layer**:

   ```bash
   zip -r9 layer.zip python
   ```

4. **Create a Lambda Layer in AWS**:

   - Go to the [AWS Lambda Console](https://console.aws.amazon.com/lambda/).
   - Click on **Layers** in the left-hand menu and then **Create layer**.
   - Name your layer (e.g., `python-dependencies`).
   - Upload the `layer.zip` file.
   - Choose the compatible runtime.
   - Click **Create**.

### Step 2: Deploy the Lambda Function

1. **Create a Deployment Package**:

   Only include your Python script since dependencies are managed by the layer.

   ```bash
   zip function.zip lambda_function.py
   ```

2. **Create a New Lambda Function**:

   - Go to the AWS Lambda console.
   - Click **Create Function**.
   - Choose **Author from scratch**.
   - Name your function (e.g., `CrossfitWorkoutFetcher`).
   - Choose the appropriate Python runtime (e.g., Python 3.12).
   - Click **Create function**.

3. **Upload the Deployment Package**:

   - Under the "Code" section, click **Upload from** and select **.zip file**.
   - Upload the `function.zip` file.

4. **Attach the Layer to the Lambda Function**:

   - Scroll down to the **Layers** section and click **Add a layer**.
   - Choose **Custom layers** and select your previously created layer (`python-dependencies`).
   - Click **Add**.

5. **Configure the Lambda Function Handler**:

   Ensure the **Handler** field is set to `lambda_function.lambda_handler` (or adjust according to your script name).

6. **Test the Lambda Function**:

   - Click **Test** in the AWS Lambda console.
   - Configure a test event (use the default settings).
   - Click **Test** to run the function and check the output.

### Step 3: Expose the function using Function URL (optional)

- In the Configuration tab of your Lambda function, find the Function URL section.
- Click **Create function URL**.
- Choose Auth type as None (if you want the function to be publicly accessible) or AWS IAM for restricted access.
- Click Create function URL.

## Additional Notes

- **Ensure Python Version Compatibility**: The Python version in your Lambda function and the Lambda layer must match.
- **Error Handling**: Use CloudWatch Logs to debug and troubleshoot any errors that occur in your Lambda function.
- **Security Best Practices**: Restrict API Gateway access using AWS IAM roles or API keys if exposing sensitive data.
- **Testing**: Create suites for testing your code before creating a new version and deploying it to prod
