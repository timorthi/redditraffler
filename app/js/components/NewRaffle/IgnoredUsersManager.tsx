import React, { useState } from "react";
import { useFormContext } from "react-hook-form";
import {
  Field,
  Control,
  Input,
  Label,
  Help,
} from "react-bulma-components/lib/components/form";
import Button from "react-bulma-components/lib/components/button";

import { colors } from "@js/theme";

const IgnoredUsersManager: React.FC = () => {
  const { control } = useFormContext();
  const [currentTextInput, setCurrentTextInput] = useState<string>("");
  const [isCurrentUsernameValid, setIsCurrentUsernameValid] = useState<boolean>(
    false
  );
  const [ignoredUsersList, setIgnoredUsersList] = useState<Array<string>>([]);

  const shouldShowValidationError =
    currentTextInput !== "" && !isCurrentUsernameValid;

  /**
   * Returns if a username is a valid Reddit username and checks whether
   * that user is already ignored.
   * @param username The username to test
   */
  const isValidUsername = (username: string) => {
    const USERNAME_REGEX = /^[\w-]+$/;
    const ignoredUsersSetLowercase = new Set(
      ignoredUsersList.map((user) => user.toLowerCase())
    );
    return (
      username.length >= 3 &&
      username.length <= 20 &&
      USERNAME_REGEX.test(username) &&
      !ignoredUsersSetLowercase.has(username)
    );
  };

  const addIgnoredUser = (user: string) => {
    setIsCurrentUsernameValid(true);
    setIgnoredUsersList([...ignoredUsersList, user]);
    setCurrentTextInput(""); // Clear input on successful add
  };

  return (
    <React.Fragment>
      <Label style={{ color: colors.reddit }}>Ignored Users</Label>
      <Help style={{ paddingBottom: "1rem" }}>
        Use this field to add usernames, such as the submission&apos;s author or
        bots like <code>AutoModerator</code>, that you want to exclude from this
        raffle.
        <br />
        Usernames are case-insensitive.
      </Help>
      <Field kind="addons">
        <Control>
          <span className="button is-static">/u/</span>
        </Control>
        <Control>
          <Input
            type="text"
            color={shouldShowValidationError ? "danger" : null}
            value={currentTextInput}
            onChange={(e: React.ChangeEvent<HTMLInputElement>) => {
              setIsCurrentUsernameValid(isValidUsername(e.target.value));
              setCurrentTextInput(e.target.value);
            }}
            onKeyPress={(e: React.KeyboardEvent<HTMLInputElement>) => {
              if (e.key !== "Enter") {
                return;
              }

              e.preventDefault(); // Stop the whole form from submitting
              if (isCurrentUsernameValid) {
                addIgnoredUser(currentTextInput);
              }
            }}
          />
        </Control>
        <Control>
          <Button
            disabled={!isCurrentUsernameValid}
            style={{ backgroundColor: colors.reddit, color: "whitesmoke" }}
            onClick={() => addIgnoredUser(currentTextInput)}
            onKeyPress={(e: React.KeyboardEvent<HTMLButtonElement>) => {
              if (e.key === "Enter") {
                addIgnoredUser(currentTextInput);
              }
            }}
          >
            Ignore
          </Button>
        </Control>
      </Field>
      {shouldShowValidationError && (
        <Help color="danger">
          This is not a valid Reddit username, or it is already in the list of
          ignored users.
        </Help>
      )}
      {ignoredUsersList.map((user) => (
        <p key={user}>{user}</p>
      ))}
    </React.Fragment>
  );
};

export default IgnoredUsersManager;
