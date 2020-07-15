
doc = '''
#%RAML 1.0
title: codenation-python-semana-8
version: v0.1
mediaType: application/json

securitySchemes:
  JWT:
    description: Use this to any method that needs a valid JWT.
    type: x-{other}
    describedBy:
      headers:
        Authorization:
            description: X-AuthToken
            type: string
            required: true
      responses:
        201:
          body: 
            application/json:
              description: Token generated
        400:
          body: 
            application/json:
              description: Token expired
    settings:
      signatures: ['HS256']

types:
  Auth:
    type: object
    discriminator: token
    properties:
      token : string
  
  User:
    type: object
    discriminator: name
    properties:
      user_id: integer
      group_id: integer
      name:
        type: string
        required: true
        maxLength: 50
      password:
        type: string
        required: true
        maxLength: 50
      email:
        type: string
        maxLength: 254
      last_login: date-only
    example:
      user_id: 1
      group_id: 1
      name: Joseph Fake
      password: "12345"
      email: email@email.com
      last_login: 2020-07-01
  
  Agent:
    type: object
    discriminator: environment
    properties: 
      agent_id: integer
      user_id: integer
      name:
        type: string
        required: true
        maxLength: 50
      status:
        type: boolean
        required: true
      environment:
        type: string
        required: true
        maxLength: 20
      version:
        type: string
        required: true
        maxLength: 5
      address:
        type: string
        maxLength: 39
    example:
      agent_id: 1
      user_id: 1
      name: linux-server
      status: true
      environment: production
      version: 1.1.1
      address: 10.0.34.15

  Event:
    type: object
    discriminator: level
    properties: 
      event_id: integer
      agent_id:
        type: integer
        required: true
      level:
        type: string
        required: true
        maxLength: 20
        enum: [critical, debug, error, warning, info]
      payload:
        type: string
        required: true
      shelved:
        type: boolean
        required: true
      data:
        type: datetime
        required: true
    example:
      event_id: 1
      agent_id: 1
      level: critical
      payload: "{example}"
      shelved: true
      data: 2020-07-01T19:54:34Z
  
  Group:
    type: object
    discriminator: name
    properties:
      group_id: integer
      name:
        type: string
        required: true
        maxLength: 20
    example:
      group_id: 1
      name: admin
  
  Message:
    type: object
    properties:
      message: string

/auth/token:
  post:
    description: Generate token
    body: 
      application/json:
        properties: 
          username: string
          password: string
    responses:
      201:
        body: 
          application/json:
            type: Auth
      400:
        body: 
          application/json:
            type: Message

/agents:
  get:
    securedBy: JWT
    description: Returns a list of agents
    responses: 
      200:
        body: 
          application/json:
            type: Agent[]
      401:
        body: 
          application/json:
            type: Message
            example:
              message: "Error: Unauthorized"
  post:
    securedBy: JWT
    description: Creates an agent
    body: 
      application/json:
        type: Agent
    responses: 
      201:
        body: 
          application/json:
            type: Message
            example:
              message: Agent successfully created
      400:
        body:
          application/json:
            type: Message
            example:
              message: Some validation error
      401:
        body: 
          application/json:
            type: Message
            example:
              message: "Error: Unauthorized"
  /{id}:
    get:
      securedBy: JWT
      description: Returns a specific agent
      responses: 
        200:
          body: 
            application/json:
              type: Agent
        401:
          body: 
            application/json:
              type: Message
              example:
                message: "Error: Unauthorized"
        404:
          body: 
            application/json:
              type: Message
              example:
                message: "Error: Agent not found"
    put:
      securedBy: JWT
      description: Updates an agent
      body: 
        application/json:
          type: Agent
      responses: 
        200:
          body: 
            application/json:
              type: Message
              example:
                message: Agent successfully updated
        400:
          body:
            application/json:
              type: Message
              example:
                message: Some validation error
        401:
          body: 
            application/json:
              type: Message
              example:
                message: "Error: Unauthorized"
        404:
          body: 
            application/json:
              type: Message
              example:
                message: "Error: Agent not found"
    delete:
      securedBy: JWT
      description: Deletes an agent
      responses: 
        200:
          body: 
            application/json:
              type: Message
              example:
                message: Agent successfully deleted
        400:
          body:
            application/json:
              type: Message
              example:
                message: Some validation error
        401:
          body: 
            application/json:
              type: Message
              example:
                message: "Error: Unauthorized"
        404:
          body: 
            application/json:
              type: Message
              example:
                message: "Error: Agent not found"
  /{id}/events:
    get:
      securedBy: JWT
      description: Returns the events linked to a specific agent
      responses: 
        200:
          body: 
            application/json:
              type: Event[]
        401:
          body: 
            application/json:
              type: Message
              example:
                message: "Error: Unauthorized"
        404:
          body: 
            application/json:
              type: Message
              example:
                message: "Error: Event not found"
    post:
      securedBy: JWT
      description: Creates an event
      body: 
        application/json:
          type: Event
      responses: 
        201:
          body: 
            application/json:
              type: Message
              example:
                message: Event successfully created
        400:
          body:
            application/json:
              type: Message
              example:
                message: Some validation error
        401:
          body: 
            application/json:
              type: Message
              example:
                message: "Error: Unauthorized"
  /{id}/events/{id}:
    get:
      securedBy: JWT
      description: Returns a specific event linked to an agent
      responses: 
        200:
          body: 
            application/json:
              type: Event
        401:
          body: 
            application/json:
              type: Message
              example:
                message: "Error: Unauthorized"
        404:
          body: 
            application/json:
              type: Message
              example:
                message: "Error: Event not found"
    put:
      securedBy: JWT
      description: Updates an event
      body: 
        application/json:
          type: Event
      responses: 
        200:
          body: 
            application/json:
              type: Message
              example:
                message: Event successfully updated
        400:
          body:
            application/json:
              type: Message
              example:
                message: Some validation error
        401:
          body: 
            application/json:
              type: Message
              example:
                message: "Error: Unauthorized"
        404:
          body: 
            application/json:
              type: Message
              example:
                message: "Error: Event not found"
    delete:
      securedBy: JWT
      description: Deletes an event
      responses: 
        200:
          body: 
            application/json:
              type: Message
              example:
                message: Event successfully deleted
        400:
          body:
            application/json:
              type: Message
              example:
                message: Some validation error
        401:
          body: 
            application/json:
              type: Message
              example:
                message: "Error: Unauthorized"
        404:
          body: 
            application/json:
              type: Message
              example:
                message: "Error: Event not found"

/groups:
  get:
    securedBy: JWT
    description: Returns a list of groups
    responses: 
      200:
        body: 
          application/json:
            type: Group[]
      401:
          body: 
            application/json:
              type: Message
              example:
                message: "Error: Unauthorized"
  post:
    securedBy: JWT
    description: Creates a group
    body: 
      application/json:
        type: Group
    responses: 
      201:
        body: 
          application/json:
            type: Message
            example:
              message: Group successfully created
      400:
        body:
          application/json:
            type: Message
            example:
              message: Name is required
      401:
          body: 
            application/json:
              type: Message
              example:
                message: "Error: Unauthorized"
  /{id}:
    get:
      securedBy: JWT
      description: Returns a specific group
      responses: 
        200:
          body: 
            application/json:
              type: Group
        401:
          body: 
            application/json:
              type: Message
              example:
                message: "Error: Unauthorized"
        404:
          body: 
            application/json:
              type: Message
              example:
                message: "Error: Group not found"
    put:
      securedBy: JWT
      description: Updates a group
      body: 
        application/json:
          type: Group
      responses: 
        200:
          body: 
            application/json:
              type: Message
              example:
                message: Group successfully updated
        400:
          body:
            application/json:
              type: Message
              example:
                message: Some validation error
        401:
          body: 
            application/json:
              type: Message
              example:
                message: "Error: Unauthorized"
        404:
          body: 
            application/json:
              type: Message
              example:
                message: "Error: Group not found"
    delete:
      securedBy: JWT
      description: Deletes a group
      responses: 
        200:
          body: 
            application/json:
              type: Message
              example:
                message: Group successfully deleted
        400:
          body:
            application/json:
              type: Message
              example:
                message: Some validation error
        401:
          body: 
            application/json:
              type: Message
              example:
                message: "Error: Unauthorized"
        404:
          body: 
            application/json:
              type: Message
              example:
                message: "Error: Group not found"

/users:
  get:
    securedBy: JWT
    description: Returns a list of users
    responses: 
      200:
        body: 
          application/json:
            type: User[]
      401:
          body: 
            application/json:
              type: Message
              example:
                message: "Error: Unauthorized"
  post:
    securedBy: JWT
    description: Creates a user
    body: 
      application/json:
        type: User
    responses: 
      201:
        body: 
          application/json:
            type: Message
            example:
              message: User successfully created
      400:
        body:
          application/json:
            type: Message
            example:
              message: Some validation error
      401:
          body: 
            application/json:
              type: Message
              example:
                message: "Error: Unauthorized"
  /{id}:
    get:
      securedBy: JWT
      description: Returns a specific user
      responses: 
        200:
          body: 
            application/json:
              type: User
        401:
          body: 
            application/json:
              type: Message
              example:
                message: "Error: Unauthorized"
        404:
          body: 
            application/json:
              type: Message
              example:
                message: "Error: User not found"
    put:
      securedBy: JWT
      description: Updates a user
      body: 
        application/json:
          type: Agent
      responses: 
        200:
          body: 
            application/json:
              type: Message
              example:
                message: User successfully updated
        400:
          body:
            application/json:
              type: Message
              example:
                message: Some validation error
        401:
          body: 
            application/json:
              type: Message
              example:
                message: "Error: Unauthorized"
        404:
          body: 
            application/json:
              type: Message
              example:
                message: "Error: User not found"
    delete:
      securedBy: JWT
      description: Deletes a user
      responses: 
        200:
          body: 
            application/json:
              type: Message
              example:
                message: User successfully deleted
        400:
          body:
            application/json:
              type: Message
              example:
                message: Some validation error
        401:
          body: 
            application/json:
              type: Message
              example:
                message: "Error: Unauthorized"
        404:
          body: 
            application/json:
              type: Message
              example:
                message: "Error: User not found"

'''
