Feature: Homepage
  As a user of cf.gov
  I should see certain content on the homepage

  Background:
    Given I goto URL "/"

  Scenario: Headline is correct
    Then the header should say "We’re on your side"

  Scenario: Summary figures should have been updated recently
    Then the summary figures should have been updated within 4 months

  Scenario: External Facebook link should present an interstitial page
    When I click on the Facebook link in the footer
    Then I should navigate to an external link page
