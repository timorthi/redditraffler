import React from "react";
import PropTypes from "prop-types";

type EmojiProps = Record<string, unknown> & {
  label?: string;
  symbol: string;
};

/**
 * Renders an Emoji.
 * Reference: https://medium.com/@seanmcp/%EF%B8%8F-how-to-use-emojis-in-react-d23bbf608bf7
 * @param {} props
 */
const Emoji: React.FC<EmojiProps> = (props) => (
  <span
    className="emoji"
    role="img"
    aria-label={props.label ? props.label : ""}
    aria-hidden={props.label ? "false" : "true"}
    {...props}
  >
    {props.symbol}
  </span>
);

Emoji.propTypes = {
  label: PropTypes.string,
  symbol: PropTypes.string,
};

export default Emoji;
