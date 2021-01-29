Feature: Allow certificates near expiry certificates close to expiry or have expired.

    Scenario: No allowed list
        Given no allowed list in directory
        When certificate checker is run
        Then no expired certificates should be found

    Scenario: Allow certificate by path PEM
        Given a file exists with a certificate with expiry of "-1" days
        And certificate path is added to allowed list
        When certificate checker is run
        And files exist in directory
        Then no expired certificates should be found

    Scenario: Allow certificate by base64 encoded string
        Given a encoded yaml file exists with a certificate with expiry of "-1" days
        And certificates base64 encoded string is added to allowed list
        And source cert material is removed
        When certificate checker is run
        And files exist in directory
        Then no expired certificates should be found