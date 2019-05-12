import React from 'react';
import {
    withStyles,
    Card,
    CardContent,
    CardHeader,
    Typography,
    Tabs,
    Tab
} from 'material-ui';
import { withTranslation } from 'react-i18next';
import { compose } from 'redux';
import { Domain, DevicesOther, Web } from 'material-ui-icons';
import PropTypes from 'prop-types';

import { CustomTable } from '../../components';

import { tasksCardStyle } from '../../variables/styles';

class ReleaseCard extends React.Component {
    state = {
        value: 0
    };
    handleChange = (event, value) => {
        this.setState({ value });
    };
    render() {
        const {
            classes,
            t,
            server_releases,
            client_releases,
            admin_client_releases
        } = this.props;
        return (
            <Card className={classes.card}>
                <CardHeader
                    classes={{
                        root: classes.cardHeader,
                        title: classes.cardTitle,
                        content: classes.cardHeaderContent
                    }}
                    title="Releases:"
                    action={
                        <Tabs
                            classes={{
                                flexContainer: classes.tabsContainer
                            }}
                            value={this.state.value}
                            onChange={this.handleChange}
                            indicatorClassName={classes.displayNone}
                            textColor="inherit"
                        >
                            <Tab
                                classes={{
                                    wrapper: classes.tabWrapper,
                                    rootLabelIcon: classes.labelIcon,
                                    label: classes.label,
                                    rootInheritSelected:
                                        classes.rootInheritSelected
                                }}
                                icon={<Domain className={classes.tabIcon} />}
                                label={t('SERVER')}
                            />
                            <Tab
                                classes={{
                                    wrapper: classes.tabWrapper,
                                    rootLabelIcon: classes.labelIcon,
                                    label: classes.label,
                                    rootInheritSelected:
                                        classes.rootInheritSelected
                                }}
                                icon={
                                    <DevicesOther className={classes.tabIcon} />
                                }
                                label={t('CLIENT')}
                            />
                            <Tab
                                classes={{
                                    wrapper: classes.tabWrapper,
                                    rootLabelIcon: classes.labelIcon,
                                    label: classes.label,
                                    rootInheritSelected:
                                        classes.rootInheritSelected
                                }}
                                icon={<Web className={classes.tabIcon} />}
                                label={t('PORTAL')}
                            />
                        </Tabs>
                    }
                />
                <CardContent>
                    {this.state.value === 0 && (
                        <Typography component="div">
                            <CustomTable
                                head={[
                                    { id: 'name', label: t('VERSION') },
                                    { id: 'created_at', label: t('DATE') },
                                    {
                                        id: 'description',
                                        label: t('RELEASE_NOTES')
                                    }
                                ]}
                                data={server_releases}
                            />
                        </Typography>
                    )}
                    {this.state.value === 1 && (
                        <Typography component="div">
                            <CustomTable
                                head={[
                                    { id: 'name', label: t('VERSION') },
                                    { id: 'created_at', label: t('DATE') },
                                    {
                                        id: 'description',
                                        label: t('RELEASE_NOTES')
                                    }
                                ]}
                                data={client_releases}
                            />
                        </Typography>
                    )}
                    {this.state.value === 2 && (
                        <Typography component="div">
                            <CustomTable
                                head={[
                                    { id: 'name', label: t('VERSION') },
                                    { id: 'created_at', label: t('DATE') },
                                    {
                                        id: 'description',
                                        label: t('RELEASE_NOTES')
                                    }
                                ]}
                                data={admin_client_releases}
                            />
                        </Typography>
                    )}
                </CardContent>
            </Card>
        );
    }
}

ReleaseCard.propTypes = {
    classes: PropTypes.object.isRequired,
    server_releases: PropTypes.array,
    client_releases: PropTypes.array,
    admin_client_releases: PropTypes.array
};

export default compose(withTranslation(), withStyles(tasksCardStyle))(
    ReleaseCard
);
