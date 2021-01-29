Feature: Finding certificates within files.

    Scenario: File with no expired certs.
        Given a file exists with a certificate with expiry of "365" days
        When certificate checker is run
        And files exist in directory
        Then no expired certificates should be found

    Scenario: File with 1 expiring certificate.
        Given a file exists with a certificate with expiry of "1" days
        When certificate checker is run
        Then "1" expiring certificates should be found

    Scenario: File with 1 expired certs.
        Given a file exists with a certificate with expiry of "-1" days
        When certificate checker is run
        Then "1" expired certificates should be found
        