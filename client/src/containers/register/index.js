import React from 'react'
import { Form } from 'formsy-react';
import MyInput from '../../components/Input';

const registerForm = React.createClass({
    getInitialState() {
        return { canSubmit: false };
    },
    submit(data) {
        alert(JSON.stringify(data, null, 4));
    },
    enableButton() {
        this.setState({ canSubmit: true });
    },
    disableButton() {
        this.setState({ canSubmit: false });
    },
    render() {
        return (
            <Form onSubmit={this.submit} onValid={this.enableButton} onInvalid={this.disableButton} className="login">
                <MyInput value="" name="name" title="Name"  validationError="This is not a valid name" required />
                <MyInput value="" name="email" title="Email" validations="isEmail" validationError="This is not a valid email" required />
                <MyInput value="" name="password" title="Password" type="password" required />
                <MyInput value="" name="checkbox" title="Deseja receber nossas novidades?" type="checkbox" />
                <MyInput value="" name="checkbox" title="Deseja receber novidades de nossos parceiros?" type="checkbox" />
                <button type="submit" disabled={!this.state.canSubmit}>Submit</button>
            </Form>
        );
    }
});

export default registerForm