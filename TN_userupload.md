
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