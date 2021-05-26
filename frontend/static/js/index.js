(function () {

    const ModalForm = {
        props: ['email', 'password', 'canCancel'],
        template: `
            <form action="">
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
                                autocomplete="off"
                                type="email"
                                :value="email"
                                placeholder="Your email">
                            </b-input>
                        </b-field>

                        <b-field label="Password">
                            <b-input
                                autocomplete="off"
                                type="password"
                                :value="password"
                                password-reveal
                                placeholder="Your password">
                            </b-input>
                        </b-field>

                        <b-checkbox>Remember me</b-checkbox>
                    </section>
                    <footer class="modal-card-foot">
                        <b-button
                            label="Close"
                            @click="$emit('close')" />
                        <b-button
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
                }
            }
        },
        methods: {
            submitFormLogin() {
                axios({
                    method: 'post',
                    url: '/oauth/token/',
                    context: this,
                    data: {
                        client_id: '2EJaS6QcLypGfBtoP2iFtJM6FA90DT0QfaaooIWb',
                        client_secret: 'oGwGr1fNOnBpmhLh4x72JErlzPzw3JRT4EtJFXAbVkrYqBr4TtVMQ9nbTCQN8jSm2349wa0SDed7TzUfRm2zcUbEdkOe2TjaaABUAEWVOAyTKXXS3gDvEjeCl7jTWo5b',
                        grant_type: 'password',
                        username: 'micael.duarte@sifat.com.br',
                        password: 'micael'
                    }
                }).then((results) => {
                    console.log(results)
                })
                this.isComponentModalActive = false
            }
        },
        mounted() {

        }
    })

})();