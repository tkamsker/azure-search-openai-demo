
Based on the documentation and code, I can help explain how to access the settings/configuration in the web client:
1. Access the Web Application

- In Azure: navigate to the Azure WebApp deployed by azd. The URL is printed out when azd completes (as "Endpoint"), or you can find it in the Azure portal.
- Running locally: navigate to 127.0.0.1:50505

Once in the web app:

- Try different topics in chat or Q&A context. For chat, try follow up questions, clarifications, ask to simplify or elaborate on answer, etc.
- Explore citations and sources
- Click on "settings" to try different options, tweak prompts, etc.

You can access the web app either:
Through the Azure deployed URL (printed after azd up completes)
Or locally at 127.0.0.1:50505 if running the development server

2. Access Settings


You can change many of the search parameters in the "Developer settings" in the frontend and see if results improve for your queries. The most relevant options:

![Screenshot of search options in developer settings](images/screenshot_searchoptions.png)

The settings can be found in the "Developer settings" section of the frontend UI. You should see a settings icon or button in the interface.

Available Settings Options
In the Developer settings, you'll find several configuration options including:
Search parameters
Upload options
Model configurations
Query options

4. To Enable Document Upload

## Enabling user document upload

You can enable an optional user document upload system to allow users to upload their own documents and chat with them. This feature requires you to first [enable login and document level access control](./login_and_acl.md). Then you can enable the optional user document upload system by setting an azd environment variable:

`azd env set USE_USER_UPLOAD true`

Then you'll need to run `azd up` to provision an Azure Data Lake Storage Gen2 account for storing the user-uploaded documents.
When the user uploads a document, it will be stored in a directory in that account with the same name as the user's Entra object id,
and will have ACLs associated with that directory. When the ingester runs, it will also set the `oids` of the indexed chunks to the user's Entra object id.


You'll need to:
First enable authentication (if not already enabled)
Run: azd env set USE_USER_UPLOAD true
Run: azd up to provision the necessary storage account
After deployment, the upload feature will be available in the web interface
Important Note
If you don't see the settings option or upload features, make sure:
The application is fully deployed (can take 5-10 minutes after deployment)
You're logged in (if authentication is enabled)
All necessary environment variables are set correctly
Would you like me to provide more specific details about any of these settings or configuration options?



##########################
Prompt : Here's a detailed step-by-step solution to minimize costs:

1. Initial Setup

# Login to Azure
azd auth login

# Create new environment
azd env new

2. Switch to Free App Service
# Set deployment target to App Service
azd env set DEPLOYMENT_TARGET appservice

# Use free tier (F1) for App Service
azd env set AZURE_APP_SERVICE_SKU F1

3. Configure Free Search Service
# Set Search Service to free tier
azd env set AZURE_SEARCH_SERVICE_SKU free

# Disable semantic search to avoid costs
azd env set AZURE_SEARCH_SEMANTIC_RANKER disabled

# Disable vectors to reduce costs
azd env set USE_VECTORS false

4. Use Local Parsers Instead of Azure Document Intelligence

# Enable local PDF parser
azd env set USE_LOCAL_PDF_PARSER true

# Enable local HTML parser
azd env set USE_LOCAL_HTML_PARSER true

5. Optimize Database Costs
# Use free tier of Cosmos DB
azd env set AZURE_COSMOSDB_SKU free

6. Reduce Monitoring Costs
# Use free tier of Cosmos DB
azd env set AZURE_COSMOSDB_SKU free

7. Optimize OpenAI Usage
# Reduce token capacity to minimum
azd env set AZURE_OPENAI_CHATGPT_DEPLOYMENT_CAPACITY 1
azd env set AZURE_OPENAI_EMB_DEPLOYMENT_CAPACITY 1

8. Deploy the Application
# Deploy to East US region (recommended for availability)
azd up --location eastus

Important Notes:
1. Limitations of Free Tier:


      The free tier will only scan the first two pages of each PDF.
      In our sample documents, those first two pages are just title pages,
      so you won't be able to get answers from the documents.
      You can either use your own documents that are only 2-pages long,
      or you can use a local Python package for PDF parsing by setting:

      ```shell
      azd env set USE_LOCAL_PDF_PARSER true
      ```

    **Limitation for HTML files:**

      The free tier will only scan the first two pages of each HTML file.
      So, you might not get very accurate answers from the files.
      You can either use your own files that are only 2-pages long,
      or you can use a local Python package for HTML parsing by setting:

      ```shell
      azd env set USE_LOCAL_HTML_PARSER true
      ```

2. Cost Breakdown After Implementation:
- App Service: Free (F1 tier)
- Azure AI Search: Free tier (limited to 50MB storage)
- Cosmos DB: Free tier
- OpenAI: Pay per use, but minimized with reduced capacity
- Storage: Minimal costs for stored documents
- No monitoring costs (Application Insights disabled)

3. Additional Cost-Saving Tips:
- Regularly clean up unused documents
- Use smaller document sizes
- Implement rate limiting in your application
- Consider scheduled shutdowns during non-business hours

4. Monitor Usage:
The default search service uses the "Basic" SKU
with the free semantic ranker option, which gives you 1000 free queries a month.
After 1000 queries, you will get an error message about exceeding the semantic ranker free capacity.




##########################
Prompt : please propose an way how to use upload without entra id maybe an oauth only 

##########################

Based on the documentation and code, I'll propose a simplified approach to enable document upload without using Microsoft Entra ID, using OAuth instead. Here's how to implement it:

1. First, modify the authentication settings

# Disable Entra ID specific settings
azd env set AZURE_USE_AUTHENTICATION false
azd env set AZURE_ENFORCE_ACCESS_CONTROL false

# Enable basic upload functionality
azd env set USE_USER_UPLOAD true

2. Create a new authentication configuration file
Create a new file oauth_config.py in the backend folder:

3. Modify the storage access
Create a simplified storage access file:

4. Update environment variables for deployment

# Set storage configuration
azd env set AZURE_STORAGE_CONTAINER user-documents
azd env set AZURE_STORAGE_ALLOWED_ORIGINS "*"

# Deploy the changes
azd up

5. Key Security Considerations
Implement rate limiting for uploads
Add file type validation
Set maximum file size limits
Implement virus scanning
Use secure storage access policies

6. Usage Limitations
Important Limitations:
- Maximum file size: 100MB per upload
- Supported file types: PDF, DOCX, TXT
- Storage quota: 5GB per user
- Rate limit: 10 uploads per hour

7. Cost Considerations
Reference to cost breakdown from deploy_lowcost.md:

This approach provides a simpler implementation than the full Entra ID solution while still maintaining basic security and access control. Would you like me to provide more details about any specific part of this implementation?
**Note: You'll need to:**

1. Replace YOUR_GITHUB_CLIENT_ID and YOUR_GITHUB_CLIENT_SECRET with actual values from your OAuth provider
azd env set GITHUB_CLIENT_ID "Ov23lin0Q7DVvGfmQC49"
azd env set GITHUB_CLIENT_SECRET "50701e24ecac01c411c37883bbc02e4ba1b1d69e"

2. Implement proper error handling
3. Add appropriate security headers
4. Consider implementing a caching layer for frequent access patterns


##########################
prompt : yes provide more details 
##########################


5. Add these environment variables:
# OAuth Configuration
azd env set GITHUB_CLIENT_ID "your_github_client_id"
azd env set GITHUB_CLIENT_SECRET "your_github_client_secret"

# Storage Configuration
azd env set MAX_UPLOAD_SIZE "104857600"  # 100MB in bytes
azd env set ALLOWED_FILE_TYPES "pdf,txt,docx"
azd env set UPLOAD_RATE_LIMIT "10"

# Security Configuration
azd env set SESSION_SECRET "your_secure_random_string"



##########################

azd env set AZURE_AUTH_TENANT_ID  "7237e154-50c1-4b9a-8b6c-100c90e7e542"



