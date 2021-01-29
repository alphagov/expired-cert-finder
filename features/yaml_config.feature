Feature: Finding certificates within yaml files.

    Scenario: Yaml file with no expired certs.
        Given a yaml file exists with a certificate with expiry of "365" days
        And source cert material is removed
        When certificate checker is run
        And files exist in directory
        Then no expired certificates should be found
        
    Scenario: Yaml file with no expired certs.
        Given a yaml file exists with a certificate with expiry of "1" days
        And source cert material is removed
        When certificate checker is run
        Then "1" expiring certificates should be found

    Scenario: Yaml file with 1 expired certs.
        Given a yaml file exists with a certificate with expiry of "-1" days
        And source cert material is removed
        When certificate checker is run
        Then "1" expired certificates should be found
        
    Scenario: Encoded Yaml file with no expired certs.
        Given a encoded yaml file exists with a certificate with expiry of "365" days
        And source cert material is removed
        When certificate checker is run
        And files exist in directory
        Then no expired certificates should be found
        
    Scenario: Encoded Yaml file with no expired certs.
        Given a encoded yaml file exists with a certificate with expiry of "1" days
        And source cert material is removed
        When certificate checker is run
        Then "1" expiring certificates should be found

    Scenario: Encoded Yaml file with 1 expired certs.
        Given a encoded yaml file exists with a certificate with expiry of "-1" days
        And source cert material is removed
        When certificate checker is run
        Then "1" expired certificates should be found
        