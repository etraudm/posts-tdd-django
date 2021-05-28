(function () {

    const ModalForm = {
        props: {
            value: {
                type: Object,
                required: true
            },
            canCancel: String
        },
        watch: {
            value() {
                console.log(this.value)
                this.$emit('input', this.value);
            }
        },
        template: `
            <form action="" style="width: 450px">
                <div class="modal-card" style="width: auto">
                    <header class="modal-card-head">
                        <p class="modal-card-title">Login</p>
                        <button
                            type="button"
                            class="delete"
                            @click="$emit('close')"/>
                    </header>
                    <section class="modal-card-body">
                        <b-field label="Email">
                            <b-input
                                autocomplete="new-password"
                                type="email"
                                v-model="value.email"
                                placeholder="Your email">
                            </b-input>
                        </b-field>
                        <b-field label="Password">
                            <b-input
                                autocomplete="new-password"
                                type="password"
                                v-model="value.password"
                                password-reveal
                                @keypress.native.enter="(value.email != '' && value.password != '') ? $emit('submit'): false"
                                placeholder="Your password">
                            </b-input>
                        </b-field>
                        <b-checkbox>Remember me</b-checkbox>
                    </section>
                    <footer class="modal-card-foot">
                        <b-button
                            label="Close"
                            @click="$emit('close')" />
                        <b-button :disabled="value.email == '' || value.password == ''"
                            @click="$emit('submit')"
                            label="Login"
                            type="is-primary" />
                    </footer>
                </div>
            </form>
        `,
    }

    Vue.component('modal-form', ModalForm)

    new Vue({
        el: '#app',
        data() {
            return {
                isComponentModalActive: false,
                formProps: {
                    email: '',
                    password: ''
                },
                isLoading: false,
                isFullPage: false
            }
        },
        methods: {
            submitFormLogin() {
                const form = new FormData()
                form.append('client_id', '2EJaS6QcLypGfBtoP2iFtJM6FA90DT0QfaaooIWb')
                form.append('client_secret', 'oGwGr1fNOnBpmhLh4x72JErlzPzw3JRT4EtJFXAbVkrYqBr4TtVMQ9nbTCQN8jSm2349wa0SDed7TzUfRm2zcUbEdkOe2TjaaABUAEWVOAyTKXXS3gDvEjeCl7jTWo5b')
                form.append('grant_type', 'password')
                form.append('username', this.formProps.email)
                form.append('password', this.formProps.password)

                this.isLoading = true

                setTimeout(() => {
                    axios({
                        method: 'post',
                        url: '/oauth/token/',
                        context: this,
                        headers: {'content-type': 'multipart/form-data'},
                        data: form,
                    }).then(({data}) => {
                        localStorage.setItem('access_token', data.access_token)
                        this.isComponentModalActive = false
                    }).catch(({response}) => {
                        if (response.status) {

                        } else {

                        }
                    }).then(() => {
                        this.isLoading = false
                    })
                }, 1000)

            }
        },
        mounted() {

        }
    })

})();