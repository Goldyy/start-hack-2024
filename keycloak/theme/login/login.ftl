<#import "template.ftl" as layout>
<@layout.registrationLayout displayMessage=!messagesPerField.existsError('username','password') displayInfo=realm.password && realm.registrationAllowed && !registrationDisabled??; section>
    <#if section = "header">
        ${msg("loginAccountTitle")}
    <#elseif section = "form">
        <#if realm.password>
            <form class="space-y-6" onsubmit="login.disabled = true; return true;" action="${url.loginAction}" method="post">
                <#if !usernameHidden??>
                    <div>
                        <label for="username" class="mb-2 block text-sm font-medium text-gray-900">
                            <#if !realm.loginWithEmailAllowed>${msg("username")}<#elseif !realm.registrationEmailAsUsername>${msg("usernameOrEmail")}<#else>${msg("email")}</#if>
                        </label>
                        <input
                            type="email"
                            name="username"
                            id="username"
                            tabindex="1" 
                            value="${(login.username!'')}"
                            class="block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-sm text-gray-900 focus:border-sneaky-yellow-500 focus:ring-sneaky-yellow-500"
                            placeholder="name@domain.com"
                            aria-invalid="<#if messagesPerField.existsError('username','password')>true</#if>"
                            required
                        />

                        <#if messagesPerField.existsError('username','password')>
                            <span id="input-error" aria-live="polite">
                                    ${kcSanitize(messagesPerField.getFirstError('username','password'))?no_esc}
                            </span>
                        </#if>
                    </div>
                </#if>
                <div>
                    <label for="password" class="mb-2 block text-sm font-medium text-gray-900"
                        >${msg("password")}</label
                    >
                    <input
                        type="password"
                        name="password"
                        id="password"
                        tabindex="2" 
                        placeholder="••••••••"
                        autocomplete="off"
                        class="block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-sm text-gray-900 focus:border-sneaky-yellow-500 focus:ring-sneaky-yellow-500"
                        required
                        aria-invalid="<#if messagesPerField.existsError('username','password')>true</#if>"
                    />
                    <#if usernameHidden?? && messagesPerField.existsError('username','password')>
                        <span id="input-error" aria-live="polite">
                                ${kcSanitize(messagesPerField.getFirstError('username','password'))?no_esc}
                        </span>
                    </#if>
                </div>

                
                
                <#if realm.rememberMe && !usernameHidden??>
                    <div class="flex items-start">
                        <div class="flex h-5 items-center">
                            <input
                                id="rememberMe"
                                type="checkbox"
                                value=""
                                tabindex="4" 
                                class="focus:ring-3 h-4 w-4 rounded border border-gray-300 bg-gray-50 focus:ring-sneaky-yellow-500"
                                <#if login.rememberMe??>
                                    checked
                                </#if>

                            />
                            <label for="rememberMe" class="ml-2 text-sm font-medium text-gray-900">
                                ${msg("rememberMe")}
                            </label>
                        </div>
                        <#if realm.resetPasswordAllowed>
                            <a 
                                class="ml-auto text-sm text-sneaky-yellow-900 hover:underline" 
                                tabindex="5" 
                                href="${url.loginResetCredentialsUrl}">${msg("doForgotPassword")}
                            </a>
                        </#if>
                    </div>
                </#if>

                <div>
                    <input type="hidden" id="id-hidden-input" name="credentialId" <#if auth.selectedCredential?has_content>value="${auth.selectedCredential}"</#if>/>
                  
                    <button
                        type="submit"
                        tabindex="4" name="login" type="submit"
                        class="w-full rounded-lg bg-sneaky-yellow-500 px-5 py-2.5 text-center text-sm font-medium text-black hover:bg-sneaky-yellow-500 focus:outline-none focus:ring-4 focus:ring-sneaky-yellow-500"
                    >
                        ${msg("doLogIn")}
                    </button>
                </div>
            </form>
        </#if>
    <#elseif section = "info" >
        <#if realm.password && realm.registrationAllowed && !registrationDisabled??>
            <div class="text-sm font-medium text-gray-500 ">
                <span>${msg("noAccount")}</span>
                <a 
                    class="ml-auto text-sm text-sneaky-yellow-900 hover:underline" 
                    tabindex="6" 
                    href="${url.registrationUrl}">${msg("doRegister")}</a>
            </div>
        </#if>
    <#elseif section = "socialProviders" >
        <#if realm.password && social.providers??>
            <div >
                <h4 class="my-2">${msg("identity-provider-login-label")}</h4>
                <hr/>

                <ul class="flex justify-start">
                    <#list social.providers as p>
                        <li class="rounded bg-sneaky-yellow-500">
                            <a id="social-${p.alias}" class=""
                                    type="button" href="${p.loginUrl}">
                                <#if p.iconClasses?has_content>
                                    <i class="" aria-hidden="true"></i>
                                    <span class="">${p.displayName!}</span>
                                <#else>
                                    <span class="">${p.displayName!}</span>
                                </#if>
                            </a>
                        </li>
                    </#list>
                </ul>
            </div>
        </#if>
    </#if>

</@layout.registrationLayout>
