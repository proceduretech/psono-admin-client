import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core';

import typographyStyle from '../../assets/jss/material-dashboard-react/typographyStyle';

class Warning extends React.Component {
    render() {
        const { classes, children } = this.props;
        return (
            <div
                className={classes.defaultFontStyle + ' ' + classes.warningText}
            >
                {children}
            </div>
        );
    }
}

Warning.propTypes = {
    classes: PropTypes.object.isRequired
};

export default withStyles(typographyStyle)(Warning);
