<template>
  <a-layout has-sider>
    <a-layout-sider
      :style="{
        overflow: 'auto',
        height: '100vh',
        position: 'fixed',
        left: 0,
        top: 0,
        bottom: 0,
      }"
    >
      <div class="logo">
        <img class="icon" src="/public/logo.png" alt="icon" />
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
        <a-table
          :columns="columns"
          :data-source="table_list"
          :pagination="false"
          :loading="loading"
        >
          <template #bodyCell="{ column, record }">
            <template v-if="column.key === 'bianhua'">
              <a-button
                type="link"
                v-if="+record.bianhua !== 0"
                :danger="+record.bianhua <= 0"
                >{{ record.bianhua }}</a-button
              >
            </template>
          </template>
          <template #expandedRowRender="{ record }">
            <div class="expand">
              <a-table
                :columns="sub_columns"
                :data-source="record.list"
                :pagination="false"
                :scroll="{ y: 500 }"
                style="
                  box-shadow: 0px 0px 12px rgb(0 0 0 / 12%);
                  margin-left: 0;
                "
              >
                <template #bodyCell="{ column, record }">
                  <template v-if="column.key === 'zhangdie'">
                    <a-button type="link" :danger="+record.zhangdie >= 0"
                      >{{ record.zhangdie }}%</a-button
                    >
                  </template>
                </template>
              </a-table>
            </div>
          </template>
        </a-table>
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
} from "@ant-design/icons-vue";
import { defineComponent, ref, onMounted, getCurrentInstance } from "vue";

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
    const instance: any = getCurrentInstance();
    const columns = [
      { title: "板块名称", dataIndex: "name", key: "name" },
      { title: "动量排名", dataIndex: "paiming", key: "paiming" },
      { title: "排名变化", key: "bianhua" },
      { title: "动量分值", dataIndex: "fenzhi", key: "fenzhi" },
      { title: "数量", dataIndex: "count", key: "count" },
    ];
    const sub_columns = [
      { title: "股票简称", dataIndex: "name", key: "name" },
      { title: "最新涨跌幅", key: "zhangdie" },
      { title: "所属同花顺行业", dataIndex: "hangye", key: "hangye" },
      { title: "所属概念", dataIndex: "gainian", key: "gainian", width: 400 },
    ];
    const loading = ref(false);
    const table_list = ref([]);
    const queryData = () => {
      loading.value = true;
      instance.proxy.$http
        .get("/gateway/api/get_wencai_data")
        .then((res: any) => {
          const list = res.data.data;
          table_list.value = list;
          loading.value = false;
        })
        .catch(() => {
          loading.value = false;
        });
    };

    onMounted(() => {
      queryData();
    });

    return {
      selectedKeys: ref<string[]>(["1"]),
      table_list,
      columns,
      sub_columns,
      loading,
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
.logo .icon {
  width: 46px;
  height: 46px;
  margin-right: 10px;
}
.site-layout .site-layout-background {
  background: #fff;
}

[data-theme="dark"] .site-layout .site-layout-background {
  background: #141414;
}
</style>
