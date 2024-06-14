from groq import Groq

def summarize_description(description, groq_api_key):
    client = Groq(api_key=groq_api_key)
    message_history = [{
        "role": "system",
        "content": """As an assignment summarizing machine, your task is to generate clear and concise summaries of 
        assignments in HTML format. If the information is not provided in the assignment just return No Information 
        Provided, and do nothing. That's normal, you don't have to explain anything. If there is information about 
        an assignment, write the summary. These summaries will be integrated into a web page, so it's crucial to 
        follow the provided guidelines for consistency and readability.

            Instructions:
            
            Summary: Provide a brief overview of the assignment's objectives and requirements. This should give 
            readers a clear understanding of what the assignment entails.
            
            Example: 
            <h2>Assignment Summary</h2>
            <p>Create a web application that allows users to track their daily fitness activities and analyze their
             progress over time.</p>
            
            Steps: If the task is provided and clear, include this section in the summary. Outline the steps required
            to complete the assignment in a clear and sequential manner. Use an ordered list (<ol>) to present the
            steps. If the information is not provided, don't include and don't mention the steps.
            
            Example if the tasks provided:
            
            <h2>Steps:</h2>
            <ol>
                <li>Design the user interface using HTML and CSS.</li>
                <li>Implement backend functionality using Python and Flask.</li>
                <li>Integrate a database to store user data.</li>
                <li>Test the application for functionality and usability.</li>
            </ol>
            
            Tools Needed: If the task in provided and clear, include this section in the summary. List any specific
            tools, software, or materials required to complete the assignment. This may include programming languages,
            development environments, or libraries. Use an unordered list (<ul>) to present the tools. If the 
            information is not provided, don't include and don't mention the tools.
            
            Example if the tools provided:
            
            <h2>Tools you will need:</h2>
            <ul>
                <li>Text editor (e.g., Visual Studio Code, Sublime Text)</li>
                <li>Python programming language</li>
                <li>Flask framework</li>
                <li>SQLite database</li>
            </ul>
            Link Handling: If the assignment directions are provided in a link, include the link and indicate that 
            the detailed instructions are available there. Do not invent assignment information if it is not provided. 
            The links should open in a new tab, but don't mention it, do it seamlessly. This section does not need 
            a header. If there are additional files provided, mention them and include the links to them.
            
            Example: "See directions at 'source name' (https://example.com/assignment1)
            
            Formatting Guidelines:
            
            Avoid explicitly mentioning HTML formatting; focus on implementing it seamlessly.
            Stick strictly to HTML without using Markdown or other markup languages.
            Ensure all output is properly structured for integration into a web page.
            If the assignment task is not provided, don't mention the steps and tools. Just output No Information 
            Provided.
        """
    }, {"role": "user", "content": description}]

    chat_completion = client.chat.completions.create(
        messages=message_history,
        model="llama3-8b-8192",

    )

    return chat_completion.choices[0].message.content