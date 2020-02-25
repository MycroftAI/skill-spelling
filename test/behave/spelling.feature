Feature: mycroft-spelling

  Scenario: spell test
    Given an english speaking user
     When the user says "how do you spell the word test"
     Then "mycroft-spelling" should reply with exactly "T; E; S; T"

  Scenario: spell happiness
    Given an english speaking user
     When the user says "spell happiness"
     Then "mycroft-spelling" should reply with exactly "H; A; P; P; I; N; E; S; S"
