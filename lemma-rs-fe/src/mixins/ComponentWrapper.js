export default {
    data: function() {
        return {
            dataValue: this.value
        }
    },
    props: {
        value: String
    },
    watch: {
        value: {
            immediate: true,
            handler: function(newValue) {
                this.dataValue = newValue
            }
        }
    }
}
