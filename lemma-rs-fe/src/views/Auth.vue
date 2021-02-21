<template>
    <h1>Please wait</h1>
</template>
<script>
export default {
    created(){
        window.opener.postMessage({token: 'aaa', secret: 'bbb'}, 'http://localhost:8080');
    }
}
</script>