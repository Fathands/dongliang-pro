<template>
  <a-layout has-sider>
    <a-layout-sider
      :style="{ overflow: 'auto', height: '100vh', position: 'fixed', left: 0, top: 0, bottom: 0 }"
    >
      <div class="logo">
        <img class="icon" src="/public/logo.png" alt="icon">
        Momentum
      </div>
      <a-menu v-model:selectedKeys="selectedKeys" theme="dark" mode="inline">
        <a-menu-item key="1">
          <user-outlined />
          <span class="nav-text">工作台</span>
        </a-menu-item>
      </a-menu>
    </a-layout-sider>
    <a-layout :style="{ marginLeft: '200px' }">
      <a-layout-header :style="{ background: '#fff', padding: 0 }" />
      <a-layout-content :style="{ margin: '24px 16px 0', overflow: 'initial' }">
        sss
      </a-layout-content>
      <a-layout-footer :style="{ textAlign: 'center' }">
        Momentum ©2023 Created by Hzx
      </a-layout-footer>
    </a-layout>
  </a-layout>
</template>

<script lang="ts">
import {
  UserOutlined,
  VideoCameraOutlined,
  UploadOutlined,
  BarChartOutlined,
  CloudOutlined,
  AppstoreOutlined,
  TeamOutlined,
  ShopOutlined,
} from '@ant-design/icons-vue';
import { defineComponent, ref, onMounted } from 'vue';
import axios from 'axios';


export default defineComponent({
  components: {
    UserOutlined,
    VideoCameraOutlined,
    UploadOutlined,
    BarChartOutlined,
    CloudOutlined,
    AppstoreOutlined,
    TeamOutlined,
    ShopOutlined,
  },
  setup() {
    const queryData = () => {
        axios({
          method: "post",
          url:"http://www.iwencai.com/customized/chart/get-robot-data",//请求的链接地址
          headers: {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json",
          },
          data: {
            "question":"20日涨幅从高到底排序的前350只股票；非新股非st；基金持股大于2％的个股或北上资金持股大于0.5％；按行业分类；",
            "perpage":"100",
            "page":1,
            "secondary_intent":"stock",
            "log_info":"{\"input_type\":\"typewrite\"}",
            "source":"Ths_iwencai_Xuangu",
            "version":"2.0","query_area":"",
            "block_list":"",
            "add_info":"{\"urp\":{\"scene\":1,\"company\":1,\"business\":1},\"contentType\":\"json\",\"searchInfo\":true}",
            "rsh":"438791553"},
        })
          .then((resp) => {
            //如果成功将在这里进行后续的逻辑操作
          })
          .catch((err) => {
          //如果请求失败将在这里进行后续的逻辑操作
         
          }); 
    };

    onMounted(() => {
      queryData()
    })

    return {
      selectedKeys: ref<string[]>(['1']),
    };
  },
});
</script>

<style scoped>
.logo {
  color: #ffffff;
  font-size: 18px;
  display: flex;
  align-items: center;
  padding: 10px;
}
.logo .icon{
  width: 46px;
  height: 46px;
  margin-right: 10px;
}
.site-layout .site-layout-background {
  background: #fff;
}

[data-theme='dark'] .site-layout .site-layout-background {
  background: #141414;
}
</style>
