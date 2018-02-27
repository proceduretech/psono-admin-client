/**
 * Client service for the psono web client
 */

import axios from 'axios';
import action from '../actions/boundActionCreators';
import store from './store'

function get_version() {
    const client_url = store.getState().client.url;
    return axios.get(client_url + '/VERSION.txt')
}

function set_url(url) {
    action.set_client_url(url)
}

const client = {
    get_version,
    set_url,
};

export default client;