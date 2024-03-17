<#import "template.ftl" as layout>
<@layout.registrationLayout displayInfo=true displayMessage=!messagesPerField.existsError('username'); section>
    <#if section = "header">
        ${msg("emailForgotTitle")}
    <#elseif section = "form">
        <form class="space-y-6" action="${url.loginAction}" method="post">
            <div>
                <label for="username" class="mb-2 block text-sm font-medium text-gray-900">
                    <#if !realm.loginWithEmailAllowed>${msg("username")}<#elseif !realm.registrationEmailAsUsername>${msg("usernameOrEmail")}<#else>${msg("email")}</#if>
                </label>
                <input 
                    type="text" 
                    id="username" 
                    name="username" 
                    class="block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-sm text-gray-900 focus:border-sneaky-yellow-500 focus:ring-sneaky-yellow-500" 
                    autofocus 
                    value="${(auth.attemptedUsername!'')}" 
                    aria-invalid="<#if messagesPerField.existsError('username')>true</#if>"
                    required
                />
                <#if messagesPerField.existsError('username')>
                    <span id="input-error-username" class="" aria-live="polite">
                                ${kcSanitize(messagesPerField.get('username'))?no_esc}
                    </span>
                </#if>
            </div>
            <div class="">
                <a 
                    class="ml-auto text-sm text-sneaky-yellow-900 hover:underline" 
                    tabindex="6" 
                    href="${url.loginUrl}">${kcSanitize(msg("backToLogin"))?no_esc}</a>
            </div>
            <div>
                <button
                    type="submit"
                    tabindex="4" 
                    name="login" 
                    type="submit"
                    class="w-full rounded-lg bg-sneaky-yellow-500 px-5 py-2.5 text-center text-sm font-medium text-black hover:bg-sneaky-yellow-500 focus:outline-none focus:ring-4 focus:ring-sneaky-yellow-500"
                >
                    ${msg("doSubmit")}
                </button>
            </div>
        </form>
    <#elseif section = "info" >
        <#if realm.duplicateEmailsAllowed>
            ${msg("emailInstructionUsername")}
        <#else>
            ${msg("emailInstruction")}
        </#if>
    </#if>
</@layout.registrationLayout>
