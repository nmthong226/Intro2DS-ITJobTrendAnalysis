def track_role_level(data) :
        # Define possible roles and levels with associated keywords
    role_keywords = {
        'Mobile': [
            'mobile', 'android', 'ios', 'react native', 'flutter',
            'swift', 'kotlin', 'xamarin', 'cordova', 'unity', 'unreal engine', 'game development'
        ],
        'Web': [
            'web', 'website', 'site', 'web developer', 'html', 'html5', 'css', 'css3', 'javascript',
            'node.js', 'jquery', 'angular', 'vue.js', 'bootstrap', 'sass', 'tailwind css'
        ],
        'Frontend': [
            'frontend', 'front-end', 'ui', 'ux', 'html', 'css', 'javascript', 'react', 'angular',
            'vue.js', 'bootstrap', 'sass', 'tailwind css', 'responsive design', 'ui/ux', 'seo', 
            'web design', 'figma', 'adobe xd', 'css3', 'html5'
        ],
        'Backend': [
            'backend', 'back-end', 'server', 'api', 'node.js', 'php', 'java', 'python', 'c++', 'c#',
            'express', 'nestjs', 'mongodb', 'postgresql', 'mysql', 'redis', 'mongodb', 'graphql', 'restful api',
            'spring', 'django', 'flask', 'laravel', 'ruby on rails', 'nestjs', 'docker', 'kubernetes', 'terraform',
            'aws', 'azure', 'gcp', 'grpc', 'apache', 'nginx', 'iis', 'sql', 'nosql', 'jenkins', 'ci/cd'
        ],
        'Fullstack': [
            'fullstack', 'full-stack', 'end-to-end', 'react', 'angular', 'vue.js', 'node.js', 'python', 'java',
            'express', 'mongodb', 'mysql', 'graphql', 'restful api', 'docker', 'kubernetes', 'aws', 'azure', 'gcp',
            'typescript', 'git', 'github', 'gitlab', 'bitbucket'
        ],
        'DevOps': [
            'devops', 'infrastructure', 'ci/cd', 'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'terraform', 
            'ansible', 'chef', 'puppet', 'git', 'jenkins', 'microservices', 'serverless', 'kafka', 'rabbitmq',
            'linux', 'unix', 'bash', 'shell scripting', 'monitoring', 'nagios', 'prometheus', 'elasticsearch'
        ],
        'Software': [
            'software', 'application', 'app', 'developer', 'programming', 'c++', 'java', 'python', 'c#', 'node.js',
            'php', 'swift', 'kotlin', 'xamarin', 'unity', 'game development', 'angular', 'vue.js', 'jquery', 'html',
            'css', 'sql', 'database', 'mysql', 'postgresql', 'mssql'
        ],
        'QA': [
            'qa', 'quality assurance', 'tester', 'testing', 'manual testing', 'automation testing', 'selenium',
            'pytest', 'testng', 'jenkins', 'git', 'ci/cd', 'jira', 'confluence', 'agile', 'scrum', 'kanban', 'load testing',
            'unit testing', 'functional testing', 'regression testing', 'performance testing', 'security testing'
        ],
        'Data': [
            'data', 'data analyst', 'data scientist', 'database', 'sql', 'python', 'r', 'pandas', 'numpy', 'scipy',
            'sasl', 'matlab', 'jupyter', 'hadoop', 'spark', 'big data', 'machine learning', 'deep learning',
            'ai', 'data mining', 'nosql', 'postgresql', 'mysql', 'redis', 'mongodb', 'etl', 'tableau', 'power bi',
            'qlik', 'google analytics', 'business intelligence', 'spss', 'etl', 'bigquery', 'snowflake', 'aws', 'azure'
        ],
        'AI': [
            'ai', 'artificial intelligence', 'machine learning', 'ml', 'deep learning', 'tensorflow', 'keras', 'pytorch',
            'hadoop', 'spark', 'nltk', 'scikit-learn', 'numpy', 'pandas', 'computer vision', 'reinforcement learning',
            'neural networks', 'data mining', 'chatbots', 'natural language processing', 'speech recognition',
            'opencv', 'robotics', 'image recognition'
        ],
        'Product Owner': [
            'product owner', 'po', 'product manager', 'product strategy', 'roadmap', 'stakeholder management',
            'scrum', 'agile', 'backlog', 'sprint planning', 'product backlog', 'user stories', 'ux/ui', 'customer feedback',
            'market research', 'business analysis', 'project management'
        ],
        'Team Lead': [
            'team lead', 'technical lead', 'lead developer', 'manager', 'scrum master', 'agile', 'project management',
            'mentorship', 'leadership', 'stakeholder management', 'team collaboration', 'delivery management',
            'jira', 'confluence', 'sprint planning', 'backlog grooming', 'project scoping'
        ],
        'QC': [
            'qc', 'quality control', 'inspection', 'test', 'defect', 'software testing', 'manual testing', 'automation testing',
            'quality assurance', 'compliance', 'audit', 'iso 9001', 'inspection', 'product quality'
        ],
        'Game Developer': [
            'game development', 'unity', 'unreal engine', 'c++', 'c#', 'swift', 'kotlin', 'xamarin', 'react native',
            'game design', 'game engines', 'game programming', 'multiplayer', 'augmented reality', 'virtual reality',
            'game mechanics', 'level design', 'game testing', 'game UI', 'mobile games', 'pc games', 'game assets'
        ]
    }


    levels = ['Senior', 'Fresher', 'Intern', 'Junior', 'Lead']
       
    # Check for role in the title
    for r in role_keywords:
        if r.lower() in data.title.lower():
            data.role = r
            break  # Stop once a role is found

    # Check for level in the title
    for l in levels:
        if l.lower() in data.title.lower():
            data.level = l
            break  # Stop once a level is found

    return data

