<template>
  <div class="work-bench">
    <a-space style="margin-bottom: 20px;">
      <a-button type="primary" @click="updateIndustry" :loading="btnloading">更新行业数据</a-button>
      <a-button type="primary" @click="queryData" :loading="loading">查询</a-button>
    </a-space>

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
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, getCurrentInstance } from "vue";

export default defineComponent({
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
    const btnloading = ref(false);
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

    const updateIndustry = () => {
      btnloading.value = true;
      instance.proxy.$http
        .get("/gateway/api/get_industry")
        .then((res: any) => {
          btnloading.value = false;
        })
        .catch(() => {
          btnloading.value = false;
        });
    }

    onMounted(() => {
      queryData();
    });

    return {
      table_list,
      columns,
      sub_columns,
      loading,
      updateIndustry,
      btnloading,
      queryData
    };
  },
});
</script>

