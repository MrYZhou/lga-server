// 默认的仓库
export const useMainStore = defineStore({
  //仓库标识
  id: 'main',
  // 仓库资源
  state: () => ({
    name: 'hello larry',
    tableInfo: [],
    config:{},
  }),
  // 快捷获取
  getters: {
    // 可以自己定义新的key,进行改造,相同名字会warning
    me: (state) => state.name.replace('hello', ''),
  },
  // 行为
  actions: {
    configData(data){
      this.config.renderData = data.content
      this.config.header = data.header.map(item=>{
        return {
          [item.key]:item.value
        }
      })
    },
    saveConfig(config){
      this.config = config
    },
  },
})
