### seed project

#### For development:
``` $ find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs sudo rm -rf ```

``` $ chmod +x src/entrypoint.sh ```

``` $ docker-compose up ```

### Run tests:
In separate tab

``` $ docker-compose exec django bash ```

``` $ $test  ```

Check vulnerable code of mine: ``` $ $bandit ```

Check outdated requirements: ``` $ $outdated ```

Check vulnerable requirements: ``` $ $safety ```
