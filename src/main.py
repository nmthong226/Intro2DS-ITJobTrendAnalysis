def track_role_level(data) :
        # Define possible roles and levels with associated keywords
    role_keywords = {
        'Mobile': ['mobile', 'android', 'ios', 'react native', 'flutter'],
        'Web': ['web', 'website', 'site', 'web developer'],
        'Frontend': ['frontend', 'front-end', 'ui', 'ux'],
        'Backend': ['backend', 'back-end', 'server', 'api', 'node.js', 'php', 'java', 'python'],
        'Fullstack': ['fullstack', 'full-stack', 'end-to-end'],
        'DevOps': ['devops', 'infrastructure', 'ci/cd', 'docker', 'kubernetes'],
        'Software': ['software', 'application', 'app', 'developer'],
        'QA': ['qa', 'quality assurance', 'tester', 'testing'],
        'Data': ['data', 'data analyst', 'data scientist', 'database', 'sql'],
        'AI': ['ai', 'artificial intelligence', 'machine learning', 'ml', 'deep learning'],
        'Product Owner': ['product owner', 'po', 'product manager'],
        'Team Lead': ['team lead', 'technical lead', 'lead developer', 'manager'],
        'QC': ['qc', 'quality control']
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

