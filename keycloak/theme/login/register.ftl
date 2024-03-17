<#import "template.ftl" as layout>
<@layout.registrationLayout displayMessage=!messagesPerField.existsError('firstName','lastName','email','username','password','password-confirm'); section>
    <#if section = "header">
        ${msg("registerTitle")}
    <#elseif section = "form">
        <form class="space-y-6" action="${url.registrationAction}" method="post">
            <div>
                <a 
                    href="${url.loginUrl}"
                    class="text-sneaky-yellow-900 hover:underline">
                    ${kcSanitize(msg("backToLogin"))?no_esc}
                </a>
            </div>
            <div class="mb-6 flex gap-4">
                <div class="w-1/2">
                    <label
                        for="firstName"
                        class="mb-2 block text-sm font-medium text-gray-900"
                        >${msg("firstName")}</label
                    >
                    <input

                        type="text" 
                        id="firstName" 
                        name="firstName"
                        value="${(register.formData.firstName!'')}"
                        aria-invalid="<#if messagesPerField.existsError('firstName')>true</#if>"
                        class="block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-sm text-gray-900 focus:border-sneaky-yellow-500 focus:ring-sneaky-yellow-500"
                        placeholder="${msg("firstName")}"
                        required
                        tabindex="1"
                    />
                </div>
                <div class="w-1/2">
                    <label
                        for="lastName"
                        class="mb-2 block text-sm font-medium text-gray-900"
                        >${msg("lastName")}</label
                    >
                    <input

                        type="text" 
                        id="lastName" 
                        name="lastName"
                        value="${(register.formData.lastName!'')}"
                        aria-invalid="<#if messagesPerField.existsError('lastName')>true</#if>"

                        class="block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-sm text-gray-900 focus:border-sneaky-yellow-500 focus:ring-sneaky-yellow-500"
                        placeholder="${msg("lastName")}"
                        required
                    />
                </div>
            </div>
            <div>
                <div class="w-1/2">
                    <#if messagesPerField.existsError('firstName')>
                        <span id="input-error-firstname" aria-live="polite">
                            ${kcSanitize(messagesPerField.get('firstName'))?no_esc}
                        </span>
                    </#if>
                </div>
                <div class="w-1/2">
                    <#if messagesPerField.existsError('lastName')>
                        <span id="input-error-lastname" aria-live="polite">
                            ${kcSanitize(messagesPerField.get('lastName'))?no_esc}
                        </span>
                    </#if>
                </div>
            </div>

            <div>
                <label for="email" class="mb-2 text-sm font-medium text-gray-900"
                    >${msg("email")}</label
                >
                <input
                    type="email"
                    id="email" 
                    name="email"
                    value="${(register.formData.email!'')}" 
                    autocomplete="email"
                    aria-invalid="<#if messagesPerField.existsError('email')>true</#if>"
                    class="block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-sm text-gray-900 focus:border-sneaky-yellow-500 focus:ring-sneaky-yellow-500"
                    placeholder="name@domain.com"
                    required
                />
                
                <#if messagesPerField.existsError('email')>
                    <span id="input-error-email" aria-live="polite">
                        ${kcSanitize(messagesPerField.get('email'))?no_esc}
                    </span>
                </#if>
            </div>


            <#if !realm.registrationEmailAsUsername>
                <div>
                    <label 
                        for="username" 
                        class="mb-2 text-sm font-medium text-gray-900"
                        >${msg("username")}</label>
                    <input
                        type="text" 
                        id="username" 
                        name="username"
                        value="${(register.formData.username!'')}" 
                        autocomplete="username"
                        aria-invalid="<#if messagesPerField.existsError('username')>true</#if>"
                        class="block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-sm text-gray-900 focus:border-sneaky-yellow-500 focus:ring-sneaky-yellow-500"
                        placeholder="${msg("username")}"
                        required
                    />

                    <#if messagesPerField.existsError('username')>
                        <span id="input-error-username" aria-live="polite">
                            ${kcSanitize(messagesPerField.get('username'))?no_esc}
                        </span>
                    </#if>
                </div>
            </#if>


            <#if passwordRequired??>


                <div>
                    <label 
                        for="password" 
                        class="mb-2 text-sm font-medium text-gray-900">
                        ${msg("password")}
                    </label>
                    <input
                        type="password" 
                        id="password" 
                        name="password"
                        autocomplete="new-password"
                        aria-invalid="<#if messagesPerField.existsError('password','password-confirm')>true</#if>"
                        placeholder="••••••••"
                        class="block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-sm text-gray-900 focus:border-sneaky-yellow-500 focus:ring-sneaky-yellow-500"
                        required
                    />

                    <#if messagesPerField.existsError('password')>
                        <span id="input-error-password" aria-live="polite">
                            ${kcSanitize(messagesPerField.get('password'))?no_esc}
                        </span>
                    </#if>
                </div>

                <div>
                    <label 
                        for="password-confirm" 
                        class="mb-2 text-sm font-medium text-gray-900">
                        ${msg("passwordConfirm")}
                    </label>
                    <input
                        type="password" 
                        id="password-confirm" 
                        name="password-confirm"
                        autocomplete="new-password"
                        aria-invalid="<#if messagesPerField.existsError('password','password-confirm')>true</#if>"
                        placeholder="••••••••"
                        class="block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-sm text-gray-900 focus:border-sneaky-yellow-500 focus:ring-sneaky-yellow-500"
                        required
                    />
                    <#if messagesPerField.existsError('password-confirm')>
                        <span id="input-error-password-confirm" aria-live="polite">
                            ${kcSanitize(messagesPerField.get('password-confirm'))?no_esc}
                        </span>
                    </#if> 
                </div>
            </#if>

            <#if recaptchaRequired??>
                <div class="form-group">
                    <div>
                        <div class="g-recaptcha" data-size="compact" data-sitekey="${recaptchaSiteKey}"></div>
                    </div>
                </div>
            </#if>

            
            <button
                type="submit"
                class="w-full rounded-lg bg-sneaky-yellow-500 px-5 py-2.5 text-center text-sm font-medium text-black hover:bg-sneaky-yellow-500 focus:outline-none focus:ring-4 focus:ring-sneaky-yellow-500"
            >
                ${msg("doRegister")}
            </button>
        </form>
    </#if>
</@layout.registrationLayout>