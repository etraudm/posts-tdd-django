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
                                id="email-login"
                                v-model="value.email"
                                placeholder="Your email">
                            </b-input>
                        </b-field>
                        <b-field label="Password">
                            <b-input
                                autocomplete="new-password"
                                type="password"
                                id="password-login"
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
                            id="btn-login"
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
                user: null,
                postList: [],
                post: {
                    title: '',
                    body: ''
                },
                isLoading: false,
                skeleton: false,
                isFullPage: false
            }
        },
        methods: {
            savePost() {
                if (this.user != null) {
                    this.isLoading = true
                    axios({
                        method: 'post',
                        url: '/api/v1/posts/',
                        context: this,
                        headers: {'Authorization': 'Bearer ' + localStorage.getItem('access_token')},
                        data: {
                            title: this.post.title,
                            body: this.post.body,
                            user: this.user.id
                        },
                    }).then(({data}) => {
                        this.getPosts()
                    }).catch(({response}) => {
                        if (response.status == 401) {
                            this.isComponentModalActive = true
                        }
                    }).then(() => {
                        this.isLoading = false
                    })
                } else {
                    this.isComponentModalActive = true
                }
            },
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
                        this.getUser()
                        this.getPosts()
                    }).catch(({response}) => {
                        if (response.status >= 400) {
                            this.$buefy.toast.open('Invalid credentials!')
                        }
                    }).then(() => {
                        this.isLoading = false
                    })
                }, 1000)

            },
            getUser() {
                axios({
                    method: 'get',
                    url: '/api/v1/user/',
                    context: this,
                    headers: {'Authorization': 'Bearer ' + localStorage.getItem('access_token')}
                }).then(({data}) => {
                    this.user = data
                }).catch(({response}) => {
                    if (response.status == 401) {
                        this.isComponentModalActive = true
                    }

                }).then(() => {
                    this.isLoading = false
                })
            },
            getPosts() {
                this.skeleton = true
                axios({
                    method: 'get',
                    url: '/api/v1/posts/',
                    context: this,
                    headers: {'Authorization': 'Bearer ' + localStorage.getItem('access_token')},
                }).then(({data}) => {
                    setTimeout(() => {
                        this.postList = []
                        data.forEach((post) => {
                            this.postList.push(post)
                        })
                        this.skeleton = false
                    }, 1000)
                }).catch(({response}) => {
                    if (response.status == 401) {
                        this.isComponentModalActive = true
                    }

                })
            },
            confirmDeletePost(postId) {
                this.$buefy.dialog.confirm({
                    title: 'Deleting Post',
                    message: 'Are you sure you want to <b>delete</b> this post? This action cannot be undone.',
                    confirmText: 'Delete Post',
                    type: 'is-danger',
                    hasIcon: true,
                    onConfirm: () => {
                        this.deletePost(postId)
                    }
                })
            },
            deletePost(postId) {
                this.loading = true
                axios({
                    method: 'delete',
                    url: '/api/v1/posts/' + postId + '/',
                    context: this,
                    headers: {'Authorization': 'Bearer ' + localStorage.getItem('access_token')},
                }).then(({data}) => {
                    this.$buefy.toast.open('Post deleted!')
                    this.getPosts()
                }).catch(({response}) => {
                    if (response.status == 401) {
                        this.isComponentModalActive = true
                    }
                }).then(() => {
                    this.loading = false
                })
            },
            logout() {
                localStorage.removeItem('access_token');
                window.location.reload()
            }

        },

        mounted() {
            if (!localStorage.getItem("access_token")) {
                this.isComponentModalActive = true
            } else {
                this.getUser()
                this.getPosts()
            }

        }
    })

})();