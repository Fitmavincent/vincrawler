<template>
    <div>
        <h1>Result Component</h1>
        <p>{{resultUrl}}</p>
    </div>
</template>


<script>
export default {
    mounted() {
        console.log("Result Mounted", this.resultUrl)
        this.getCrawlerResult();
    },
    data() {
        return {
            resultUrl: import.meta.env.VITE_OZB_CRAWLER_URL,
        };
    },
    methods: {
        getCrawlerResult () {
            this.axios.get(this.resultUrl)
            .then((res) => {
                console.log(res)
            })
        }
    },
}
</script>


<style lang="">
    
</style>